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
			<header className="border-b border-light-white3 bg-light-white1">
				<div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-3 px-4 py-3 sm:px-6">
					<Link to="/dashboard" className="text-lg font-bold">SidiWeb</Link>
					<nav className="flex items-center gap-1">
						{NAV.map((n) => (
							<Link
								key={n.to}
								to={n.to}
								className={`rounded-lg px-3 py-2 text-sm font-medium transition ${
									isActive(n.to)
										? 'bg-light-red1/10 text-light-red1'
										: 'text-light-white4 hover:text-light-black'
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

			<main className="mx-auto w-full max-w-7xl px-4 py-6 sm:px-6">
				{(title || actions) && (
					<div className="mb-6 flex flex-wrap items-end justify-between gap-3">
						<div>
							{title ? <h1 className="text-2xl font-bold">{title}</h1> : null}
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
