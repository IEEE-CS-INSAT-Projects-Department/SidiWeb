import { Link, useLocation, useNavigate } from 'react-router-dom'
import '../../styles-tailwind.css'
import { Button } from '../components/Button'
import { logout } from '../../modules/auth/services/authService'

const NAV = [
	{ to: '/dashboard', label: 'Dashboard' },
	{ to: '/templates', label: 'Templates' },
	{ to: '/assistant', label: 'Assistant' },
	{ to: '/media', label: 'Media' },
]

export default function AppShell({ title, subtitle, actions, children }) {
	const location = useLocation()
	const navigate = useNavigate()
	const onLogout = () => {
		logout()
		navigate('/login')
	}
	const isActive = (to) => location.pathname === to || location.pathname.startsWith(to + '/')

	return (
		<div className="min-h-screen w-full overflow-x-hidden bg-light-white2 text-light-black">
			<header className="sticky top-0 z-40 border-b border-light-white3 bg-light-white1/85 backdrop-blur-md">
				<div className="mx-auto flex max-w-7xl items-center justify-between gap-3 px-4 py-3 sm:px-6">
					<Link to="/dashboard" className="flex shrink-0 items-center gap-2">
						<span className="flex h-8 w-8 items-center justify-center rounded-xl bg-light-red1 text-sm font-bold text-white">
							S
						</span>
						<span className="text-lg font-bold tracking-tight">SidiWeb</span>
					</Link>

					<nav className="mx-2 flex flex-1 items-center gap-1 overflow-x-auto">
						{NAV.map((n) => (
							<Link
								key={n.to}
								to={n.to}
								className={`shrink-0 rounded-lg px-3 py-2 text-sm font-medium transition ${
									isActive(n.to)
										? 'bg-light-red1/10 text-light-red1'
										: 'text-light-white4 hover:bg-light-white2 hover:text-light-black'
								}`}
							>
								{n.label}
							</Link>
						))}
					</nav>

					<Button variant="outline" size="sm" onClick={onLogout}>
						Log out
					</Button>
				</div>
			</header>

			<main key={location.pathname} className="animate-rise mx-auto w-full max-w-7xl px-4 py-8 sm:px-6">
				{(title || actions) && (
					<div className="mb-6 flex flex-wrap items-end justify-between gap-3">
						<div>
							{title ? <h1 className="text-2xl font-bold sm:text-3xl">{title}</h1> : null}
							{subtitle ? <p className="mt-1 text-sm text-light-white4">{subtitle}</p> : null}
						</div>
						{actions}
					</div>
				)}
				{children}
			</main>
		</div>
	)
}
