import '../../../styles-tailwind.css'
import { Button } from '../../../shared/components/Button'
import Card from '../../../shared/components/Card'
import ResponsiveGrid from '../../../shared/layout/ResponsiveGrid'
import logo from '../../../assets/logo.png'
import heroRobot from '../../../assets/image.png'
import capabilityOne from '../../../assets/image1.png'
import capabilityTwo from '../../../assets/image2.png'
import capabilityThree from '../../../assets/image3.png'

function HomePage() {
	return (
		<main className="relative min-h-screen w-full overflow-x-hidden bg-vitrine-black1 text-vitrine-white1">
			<div className="pointer-events-none absolute inset-0">
				<div className="absolute -top-24 left-1/2 h-80 w-80 -translate-x-1/2 rounded-full bg-dark-red1/30 blur-[110px]" />
				<div className="absolute top-96 -right-30 h-72 w-72 rounded-full bg-vitrine-red1/20 blur-[120px]" />
			</div>

			<header className="relative border-b border-vitrine-grey3/70">
				<div className="mx-auto flex w-full max-w-7xl items-center justify-between px-4 py-4 sm:px-6">
					<a href="#" className="flex items-center gap-2">
						<img src={logo} alt="Sidi Web logo" className="h-8 w-auto object-contain sm:h-9" />
					</a>

					<nav className="hidden items-center gap-8 text-sm text-vitrine-grey1 md:flex">
						<a href="#features" className="transition hover:text-vitrine-white1">Features</a>
						<a href="#capabilities" className="transition hover:text-vitrine-white1">Platforms</a>
						<a href="#footer" className="transition hover:text-vitrine-white1">Showcase</a>
					</nav>

					<div className="flex items-center gap-2 sm:gap-3">
						<a href="/dashboard">
							<Button variant="login" size="sm" className="h-9! px-4! text-xs! sm:h-10! sm:px-5!">Log in</Button>
						</a>
						<Button variant="signup" size="sm" className="h-9! px-4! text-xs! sm:h-10! sm:px-5!">Sign up</Button>
					</div>
				</div>
			</header>

			<section className="relative mx-auto w-full max-w-7xl px-4 pb-12 pt-10 sm:px-6 sm:pb-16 sm:pt-14">
				<div className="grid w-full grid-cols-1 items-center justify-items-stretch gap-10 lg:grid-cols-2">
					<div className="w-full min-w-0 max-w-2xl justify-self-stretch lg:max-w-none">
						<h1 className="w-full text-4xl font-bold leading-tight tracking-tight sm:text-5xl">
							Sidi Web builds
							<br />
							websites in
							<span className="text-light-red3"> seconds.</span>
						</h1>

						<p className="mt-5 text-sm leading-6 text-vitrine-grey1 sm:text-base">
							One click with AI intelligence assistance and industry-proven workflows.
							Create websites faster than your competition.
						</p>

						<div className="mt-7 flex items-center gap-3">
							<a href="/dashboard">
								<Button variant="signup" size="sm" className="h-10! px-6!">Start</Button>
							</a>
							<Button
								variant="demo"
								size="sm"
								className="h-10! px-6! border border-vitrine-grey3 bg-vitrine-black2"
							>
								Demo
							</Button>
						</div>
					</div>

					<div className="relative flex w-full justify-center justify-self-stretch lg:justify-end">
						<div className="absolute bottom-8 left-1/2 h-44 w-44 -translate-x-1/2 rounded-full bg-dark-red1/35 blur-[70px]" />
						<img
							src={heroRobot}
							alt="Sidi assistant robot"
							className="relative w-full max-w-82.5 object-contain drop-shadow-[0_18px_32px_rgba(0,0,0,0.55)]"
						/>
					</div>
				</div>
			</section>

			<section id="features" className="border-t border-vitrine-grey3/70">
				<div className="mx-auto w-full max-w-7xl px-4 py-12 sm:px-6 sm:py-14">
					<div className="mx-auto mb-9 w-full min-w-0 max-w-2xl justify-self-stretch text-center">
						<h2 className="w-full text-3xl font-semibold tracking-tight sm:text-4xl">
							From chat to <span className="text-light-red3">reality</span>
						</h2>
						<p className="mt-3 w-full text-sm text-vitrine-grey1">
							Build your project in guided steps and launch faster with a clean pipeline.
						</p>
					</div>

					<ResponsiveGrid size="L" theme="transparent" width="full">
						<Card
							variant="dark_step"
							number="01"
							title="Describe your vision"
							description="Tell us your objective, niche and design style."
							icon={<span className="text-light-red3 text-xl">▢</span>}
							className="bg-vitrine-black2/90"
						/>
						<Card
							variant="dark_step"
							number="02"
							title="AI generation"
							description="Get a complete structure with modern sections instantly."
							icon={<span className="text-light-red3 text-xl">◈</span>}
							className="bg-vitrine-black2/90"
						/>
						<Card
							variant="dark_step"
							number="03"
							title="Customize & launch"
							description="Refine content and publish with one click."
							icon={<span className="text-light-red3 text-xl">⌘</span>}
							className="bg-vitrine-black2/90"
						/>
					</ResponsiveGrid>
				</div>
			</section>

			<section id="capabilities" className="border-t border-vitrine-grey3/70">
				<div className="mx-auto w-full max-w-7xl px-4 py-12 sm:px-6 sm:py-14">
					<div className="mb-8 flex items-end justify-between gap-3">
						<h2 className="text-2xl font-semibold tracking-tight sm:text-3xl">Powerful capabilities.</h2>
						<a href="#" className="text-xs text-light-red3 transition hover:text-light-red2">View all capabilities</a>
					</div>

					<ResponsiveGrid size="L" theme="transparent" width="full">
						<Card
							variant="dark_image"
							title="Vision websites"
							description="Visual generation with clear section hierarchy."
							imageSrc={capabilityOne}
							className="bg-vitrine-black2/90"
						/>
						<Card
							variant="dark_image"
							title="Creative portfolios"
							description="Fast concepts from prompt to polished layout."
							imageSrc={capabilityTwo}
							className="bg-vitrine-black2/90"
						/>
						<Card
							variant="dark_image"
							title="Zero coding"
							description="No-code workflow with scalable design blocks."
							imageSrc={capabilityThree}
							className="bg-vitrine-black2/90"
						/>
					</ResponsiveGrid>
				</div>
			</section>

			<section className="border-t border-vitrine-grey3/70">
				<div className="mx-auto w-full max-w-5xl px-4 py-12 sm:px-6 sm:py-16">
					<div className="relative w-full overflow-hidden rounded-3xl border border-vitrine-grey3 bg-vitrine-black2 px-6 py-14 text-center sm:px-10">
						<div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(179,19,26,0.42),transparent_64%)]" />
						<div className="relative mx-auto w-full min-w-0 max-w-2xl justify-self-stretch">
							<h3 className="w-full text-3xl font-bold leading-tight sm:text-4xl">Ready to build the future?</h3>
							<p className="mt-3 w-full text-sm text-vitrine-grey1">
								Design, deploy, iterate and grow with Sidi AI.
							</p>
							<div className="mt-7 flex items-center justify-center">
								<Button variant="signup" size="sm" className="h-10! px-7!">Start for free</Button>
							</div>
						</div>
					</div>
				</div>
			</section>

			<footer id="footer" className="border-t border-vitrine-grey3/70">
				<div className="mx-auto grid w-full justify-content max-w-7xl gap-10 px-4 py-10 sm:px-6 md:grid-cols-[1.4fr_1fr_1fr]">
					<div>
						<img src={logo} alt="Sidi Web" className="h-8 w-auto object-contain" />
						<p className="mt-4 max-w-sm text-xs leading-5 text-vitrine-grey1">
							AI website creation platform built for speed, quality and consistency.
						</p>
					</div>

					<div>
						<h4 className="text-sm font-semibold">Product</h4>
						<ul className="mt-4 space-y-2 text-xs text-vitrine-grey1">
							<li><a href="#" className="transition hover:text-vitrine-white1">Features</a></li>
							<li><a href="#" className="transition hover:text-vitrine-white1">Templates</a></li>
							<li><a href="#" className="transition hover:text-vitrine-white1">Pricing</a></li>
						</ul>
					</div>

					<div>
						<h4 className="text-sm font-semibold">Company</h4>
						<ul className="mt-4 space-y-2 text-xs text-vitrine-grey1">
							<li><a href="#" className="transition hover:text-vitrine-white1">About</a></li>
							<li><a href="#" className="transition hover:text-vitrine-white1">Careers</a></li>
							<li><a href="#" className="transition hover:text-vitrine-white1">Contact</a></li>
						</ul>
					</div>
				</div>

				<div className="border-t border-vitrine-grey3/60 py-4 text-center text-[11px] text-vitrine-grey1">
					Copyright 2026 Sidi Web. All rights reserved.
				</div>
			</footer>
		</main>
	)
}

export default HomePage
